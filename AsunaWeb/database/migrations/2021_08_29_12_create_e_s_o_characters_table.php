<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateESOCharactersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('e_s_o_characters', function (Blueprint $table)
        {
            $table->id('esoCharacterID');
            $table->timestamps();
            $table->foreignId('esoUserID');
            $table->string('characterName', 20);
            $table->foreignId('roleID');
            $table->string('characterClass');
            $table->foreignId('characterRaceID');
            $table->unsignedInteger('highestDPS')->nullable();
            $table->boolean('isCertified')->default(false);

            $table->foreign('esoUserID')->references('esoUserID')->on('e_s_o_users');
            $table->foreign('roleID')->references('roleID')->on('roles');
            $table->foreign('characterRaceID')->references('characterRaceID')->on('character_races');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('e_s_o_characters');
    }
}