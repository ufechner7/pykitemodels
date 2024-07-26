using Test

cd("..")
include("test_steady_state.jl")

lift, drag = KiteModels.lift_drag(kps)

@testset "PyKiteModels" begin
    @test lift ≈ 563.1301363894148
    @test drag ≈ 127.91137175090972

end

