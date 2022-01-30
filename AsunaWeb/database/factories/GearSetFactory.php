<?php

namespace Database\Factories;

use App\Models\GearSet;
use Illuminate\Database\Eloquent\Factories\Factory;

class GearSetFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = GearSet::class;

    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'gear_set_id'
        ];
    }
}
