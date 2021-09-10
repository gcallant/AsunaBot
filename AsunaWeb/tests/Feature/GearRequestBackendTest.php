<?php

namespace Tests\Feature;

use App\Models\GearPiece;
use App\Models\GearRequest;
use App\Models\GearSet;
use App\Models\GuildMember;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class GearRequestBackendTest extends TestCase
{
//    use RefreshDatabase;
//    use DatabaseMigrations;

    /**
     * @test
     */
    public function a_guild_member_can_make_a_gear_request()
    {
//        $this->artisan('migrate:fresh --seed');
        $member = GuildMember::factory()->create();

        // Retrieve a random set
        $gearSet = GearSet::find(random_int(1, 500));

        $gearRequest = GearRequest::create(['guild_member_id' => $member->id, 'gear_set_id' => $gearSet->id]);
        $gearPiece = GearPiece::find(random_int(1, 23));
        $gearPiece->gearRequest()->attach($gearRequest->id, ['is_active' => true]);

        $this->assertDatabaseHas('gear_requests', [
            'guild_member_id' => $member->id,
            'gear_set_id' => $gearSet->id
        ]);

        $this->assertDatabaseHas('gear_piece_gear_request', [
            'gear_request_id' => $gearRequest->id,
            'gear_piece_id' => $gearPiece->id,
            'is_active' => true
        ]);
    }
}
