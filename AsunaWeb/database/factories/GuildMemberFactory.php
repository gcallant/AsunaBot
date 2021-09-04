<?php

namespace Database\Factories;

use App\Models\GuildMember;
use Illuminate\Database\Eloquent\Factories\Factory;
use JetBrains\PhpStorm\ArrayShape;

class GuildMemberFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = GuildMember::class;

    /**
     * Define the model's default state.
     *
     * @return array
     * @noinspection PhpUnhandledExceptionInspection
     * @throws \JsonException
     */
    #[ArrayShape(['name' => "string", 'discord_user_id' => "int", 'discord_role_ids' => "string"])]
    public function definition(): array
    {
        return [
            'name' => $this->faker->monthName . $this->faker->safeColorName . $this->faker->firstNameMale,
            'discord_user_id' => $this->faker->numberBetween(9, true),
            'discord_role_ids' => $this->generateRandomDiscordRolesList()
        ];
    }

    private function generateRandomDiscordRolesList(): string
    {
        /** @noinspection PhpUnhandledExceptionInspection */
        return json_encode([
                               'AwesomeRole' => $this->faker->randomNumber(9, true),
                               'OkayRole' => $this->faker->randomNumber(9, true),
                               'GreatRole' => $this->faker->randomNumber(9, true),
                               'TrialRole' => $this->faker->randomNumber(9, true),
                               'Shieldbreaker' => $this->faker->randomNumber(9, true),
                               'Valkyrie' => $this->faker->randomNumber(9, true),
                               'Citizen' => $this->faker->randomNumber(9, true),
                               'Skeever' => $this->faker->randomNumber(9, true)
                           ],
                           JSON_THROW_ON_ERROR);
    }
}
