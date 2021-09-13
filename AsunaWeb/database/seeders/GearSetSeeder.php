<?php

namespace Database\Seeders;

use App\Models\GearSet;
use App\Models\Location;
use App\Models\LocationType;
use Illuminate\Database\QueryException;
use Illuminate\Database\Seeder;
use SimpleXLSX;

/**
 * Used to seed new gear sets on DB migration, and on patch updates
 * @see https://github.com/shuchkin/simplexlsx
 */
class GearSetSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run() : void
    {
        // Removes all duplicates in a <K,V> array
        $sets = array_unique($this->parseSets(), SORT_REGULAR);

        $this->insertSets($sets);
    }

    /**
     * Parses the lib sets worksheet to extract the set and location from columns 2 and 16
     *
     * @return array of <Set, Location>
     */
    private function parseSets() : array
    {
        $sets = [];
        if ($xlsx = SimpleXLSX::parse('database/seeders/LibSets_SetData.xlsx'))
        {

            $rows = $xlsx->rows();
            foreach ($rows as $r => $row)
            {
                if ($r > 1)
                {
                    // We only want sets and location name columns in the game
                    if ($row[2] === '' || $row[16] === '' || $row[5] === 'Not in the game (anymore)')
                    {
                        continue;
                    }

                    $temp = array();
                    $temp['gear_set_name'] = $row[2];

                    // Strip the lib sets info, and find the corresponding location type ID
                    $typeID = LocationType::getID(str_replace('LIBSETS_SETTYPE_', '', $row[6]));

                    $temp['location_id'] = Location::getID($row[16], $typeID);

                    $sets[] = $temp;
                }
            }
        }
        return $sets;
    }

    /**
     * Creates a new gear set for each UQ(Set, locationID), eats UQ integrity violation
     * @param array $uniqueSets A unique <K,V> pair array of sets and location ids
     */
    private function insertSets(array $uniqueSets) : void
    {
        foreach ($uniqueSets as $set)
        {
            try
            {
                // We're using create here to populate the audit columns, as insert bypasses audit columns
                GearSet::create([
                                     'gear_set_name' => $set['gear_set_name'],
                                     'location_id' => $set['location_id'],
                                 ]);
            }
            catch (QueryException $ignore)
            {
                // We don't want to insert duplicate data, but we want process to continue
            }
        }
    }
}
