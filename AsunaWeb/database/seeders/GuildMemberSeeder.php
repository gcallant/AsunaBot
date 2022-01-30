<?php

namespace Database\Seeders;

use App\Models\GuildMember;
use Illuminate\Database\Seeder;

class GuildMemberSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run(): void
    {
        GuildMember::factory()->count(10)->create();
    }
}
