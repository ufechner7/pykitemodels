using KiteModels, KitePodModels, Oxygen, HTTP, StructTypes, JSON3

set::Settings = deepcopy(se())
dt::Float64 = 1/set.sample_freq

kcu::Union{KCU, Nothing}  = nothing
kps4::Union{KPS4, Nothing} = nothing

ex = nothing

mutable struct StepParams
    v_ro::Union{Float64, Nothing}
    set_torque::Union{Float64, Nothing}
    v_wind_gnd::Float64
    wind_dir::Float64
    depower::Float64
    steering::Float64
end

# Add a supporting struct type definition so JSON3 can serialize & deserialize automatically
StructTypes.StructType(::Type{Settings}) = StructTypes.Mutable()
StructTypes.StructType(::Type{SysState}) = StructTypes.Struct()
StructTypes.StructType(::Type{StepParams}) = StructTypes.Struct()

function set_set(dict)
    global set
    for (key, value) in dict
        # set field  of the struct with the name key to the corresponding value
        setproperty!(set, Symbol(key), value)
    end
    set
end

function init()
    global kcu, kps4, integrator
    kcu = KCU(set)
    kps4 = KPS4(kcu)
    integrator = KiteModels.init_sim!(kps4, stiffness_factor=0.5, prn=false)
    nothing
end

function start_server(log=true)
    global kcu, kps4, integrator
    @get "/sys_state" function(req::HTTP.Request)
        if isnothing(kcu) || isnothing(kps4)
            return "\"Error: system not initialized\""
        end
        state = SysState(kps4)
        state.time = integrator.t
        return json(state)
    end

    @get "/settings" function(req::HTTP.Request)
        return json(set)
    end

    @get "/init" function(req::HTTP.Request)
        init()
        return json("OK")
    end

    @post "/step" function(req::HTTP.Request)
        local res
        if isnothing(kcu) || isnothing(kps4)
            return "\"Error: system not initialized\""
        end
        p = json(req, StepParams)
        if isnothing(p.v_ro)
            p.v_ro = 0
        end
        res = "OK"
        try
            set_depower_steering(kcu, p.depower, p.steering)
            KiteModels.next_step!(kps4, integrator; p.v_ro, p.v_wind_gnd, p.wind_dir, dt=dt)
        catch e
            println(e)
            res = repr(e)
        end
        replace(res, "\"" => "'")
        return json(res)
    end

    @post "/set_set" function(req::HTTP.Request)
        str = String(req.body)
        set_set(JSON3.read(str))
        return "\"OK\""
    end

    @post "/set_data_path" function(req::HTTP.Request)
        str = String(req.body)
        data_path = JSON3.read(str)
        set_data_path(data_path)
        return "\"OK\""
    end

    # start the web server
    if log
        serve()
    else
        serve(access_log=nothing)
    end
end

function test(init_=true)
    if init_
        init()
    end
    p = StepParams(nothing, nothing, 6, 0, 0.25, 0)
    if isnothing(p.v_ro)
        p.v_ro = 0
    end
    set_depower_steering(kcu, p.depower, p.steering)
    time = KiteModels.next_step!(kps4, integrator; p.v_ro, p.v_wind_gnd, p.wind_dir, dt=dt)
    @assert time >= 0.05
    state = SysState(kps4)
    state.time = time
    state
end

function test2()
    local time, state, res
    init()
    p = StepParams(nothing, nothing, 6, 0, 0.25, 0)
    if isnothing(p.v_ro)
        p.v_ro = 0
    end
    res = "OK"
    for i in 1:30/dt
        try
            set_depower_steering(kcu, p.depower, p.steering)
            time = KiteModels.next_step!(kps4, integrator; p.v_ro, p.v_wind_gnd, p.wind_dir, dt=dt)
        catch e
            println(e)
            res = repr(e)
            break
        end
        @assert time >= 0.05
        state = SysState(kps4)
        state.time = time
    end
    res
end

start_server(false) # use start_server(false) to disable logging
# state = test()
nothing