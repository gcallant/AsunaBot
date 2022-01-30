<?php

namespace Tests\Feature;

use App\Models\GuildMember;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

class EventCreationBackendTest extends TestCase
{
    /** @test */
    public function an_authorized_guild_member_can_create_an_event()
    {
        $member = GuildMember::factory()->create();
    }
}
