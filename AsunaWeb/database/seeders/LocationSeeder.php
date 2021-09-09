<?php

namespace Database\Seeders;

use App\Models\Location;
use App\Models\LocationType;
use Illuminate\Database\QueryException;
use Illuminate\Database\Seeder;
use SimpleXLSX;

/**
 * Used to seed new locations on DB migration, and on patch updates
 * @see https://github.com/shuchkin/simplexlsx
 */
class LocationSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run() : void
    {
        // Removes all duplicates in a <K,V> array
        $uniqueLocations = array_unique($this->parseLocations(), SORT_REGULAR);

        $this->insertLocations($uniqueLocations);
    }

    /**
     * Parses the lib sets worksheet to extract the location and type from columns 6 and 16
     *
     * @return array of <TypeID, Location>
     */
    private function parseLocations() : array
    {
        $locations = [];
        if ($xlsx = SimpleXLSX::parse('database/seeders/LibSets_SetData.xlsx'))
        {

            $rows = $xlsx->rows();
            foreach ($rows as $r => $row)
            {
                if ($r > 1)
                {
                    // We only want location types and location name columns
                    if ($row[6] === '' || $row[16] === '')
                    {
                        continue;
                    }

                    $temp = array();
                    $temp['location_name'] = $row[16];

                    // Strip the lib sets info, and find the corresponding location type ID
                    $temp['location_type_id'] = LocationType::getID(str_replace('LIBSETS_SETTYPE_', '', $row[6]));

                    $locations[] = $temp;
                }
            }
        }
        return $locations;
    }

    /**
     * Creates a new location for each UQ(Location, typeID), eats UQ integrity violation
     * @param array $uniqueLocations A unique <K,V> pair array of locations and type ids
     */
    private function insertLocations(array $uniqueLocations) : void
    {
        foreach ($uniqueLocations as $location)
        {
            try
            {
                // We're using create here to populate the audit columns, as insert bypasses audit columns
                Location::create([
                                     'location_name' => $location['location_name'],
                                     'location_type_id' => $location['location_type_id'],
                                 ]);
            }
            catch (QueryException $ignore)
            {
                // We don't want to insert duplicate data, but we want process to continue
            }
        }
    }
}
