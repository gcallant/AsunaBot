<?php

namespace Database\Seeders;

use App\Models\Guild;
use App\Models\GuildMember;
use Illuminate\Database\Seeder;

class GuildBridgeMemberSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run(): void
    {
        $guilds = Guild::all();
        $members = GuildMember::all();

        foreach ($guilds as $guild)
        {
            foreach($members as $member)
            {
                $guild->guildMember()->attach($member->id);
            }
        }
    }
}
