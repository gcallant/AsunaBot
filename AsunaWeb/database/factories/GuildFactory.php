<?php

namespace Database\Factories;

use App\Models\Guild;
use Illuminate\Database\Eloquent\Factories\Factory;
use JetBrains\PhpStorm\ArrayShape;

class GuildFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = Guild::class;

    /**
     * Define the model's default state.
     *
     * @return array
     */
    #[ArrayShape(['guild_name' => "string", 'create_event_role' => "int", 'admin_role' => "int"])]
    public function definition(): array
    {
        return [
            'guild_name' => $this->faker->firstNameFemale . $this->faker->colorName . $this->faker->monthName,
            'create_event_role' => $this->faker->randomNumber(9, true),
            'admin_role' => $this->faker->randomNumber(9, true)
        ];
    }
}
