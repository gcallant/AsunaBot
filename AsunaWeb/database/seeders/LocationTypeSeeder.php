<?php

namespace Database\Seeders;

use App\Models\LocationType;
use Illuminate\Database\Seeder;

class LocationTypeSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        if(LocationType::find(1) === null)
        {
            $locationTypes = [
                'ARENA',
                'BATTLEGROUND',
                'CRAFTED',
                'CYRODIIL',
                'DAILYRANDOMDUNGEONANDICREWARD',
                'DUNGEON',
                'IMPERIALCITY',
                'MONSTER',
                'OVERLAND',
                'SPECIAL',
                'TRIAL',
                'MYTHIC'
            ];
            foreach ($locationTypes as $type)
            {
                LocationType::create(['type_name' => $type]);
            }
        }
    }
}
