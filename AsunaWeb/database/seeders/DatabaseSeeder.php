<?php

namespace Database\Seeders;

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
                        LocationSeeder::class
                    ]);
    }
}
