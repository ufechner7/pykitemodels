using Test

cd("..")
include("test_steady_state.jl")

lift, drag = KiteModels.lift_drag(kps)

@testset "PyKiteModels" begin
    @test isapprox(lift, 434.25661213474916; atol=56)
    @test isapprox(drag, 127.91137175090972; atol=28)

end

