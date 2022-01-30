<?php

namespace Database\Seeders;

use App\Models\GearSet;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run() : void
    {
        $this->call([
                        GuildSeeder::class,
                        GuildMemberSeeder::class,
                        GuildBridgeMemberSeeder::class,
                        LocationTypeSeeder::class,
                        LocationSeeder::class,
                        GearPieceSeeder::class,
                        GearSetSeeder::class
                    ]);
    }
}
