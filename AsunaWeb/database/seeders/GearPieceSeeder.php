<?php

namespace Database\Seeders;

use App\Models\GearPiece;
use Illuminate\Database\Seeder;

class GearPieceSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        if(GearPiece::find(1) === null)
        {
            $pieces = [
                'Head',
                'Shoulders',
                'Chest',
                'Hands',
                'Belt',
                'Pants',
                'Shoes',
                'Necklace',
                'Ring left',
                'Ring right',
                'Inferno staff',
                'Lightning staff',
                'Ice staff',
                'Restoration staff',
                'Shield',
                'Dagger',
                'Mace',
                'Sword',
                'Axe',
                'Greatsword',
                'Battle axe',
                'Maul',
                'Bow'
            ];

            foreach ($pieces as $piece)
            {
                GearPiece::create(['gear_piece_name' => $piece]);
            }
        }
    }
}
