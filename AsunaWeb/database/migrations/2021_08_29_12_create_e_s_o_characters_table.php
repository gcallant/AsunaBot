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
            $table->id();
            $table->timestamps();
            $table->foreignId('eso_user_id');
            $table->string('character_name', 20);
            $table->foreignId('role_id');
            $table->string('character_class');
            $table->foreignId('character_race_id');
            $table->unsignedInteger('highest_dps')->nullable();
            $table->boolean('is_certified')->default(false);

            $table->foreign('eso_user_id')->references('id')->on('e_s_o_users');
            $table->foreign('role_id')->references('id')->on('roles');
            $table->foreign('character_race_id')->references('id')->on('character_races');
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
