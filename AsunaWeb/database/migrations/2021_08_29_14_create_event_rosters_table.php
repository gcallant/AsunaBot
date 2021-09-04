<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateEventRostersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('event_rosters', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->foreignId('event_id')->unique();
            $table->unsignedTinyInteger('max_tanks')->nullable();
            $table->unsignedTinyInteger('max_heals')->nullable();
            $table->unsignedTinyInteger('max_ranged_dps')->nullable();
            $table->unsignedTinyInteger('max_melee_dps')->nullable();
            $table->unsignedTinyInteger('signed_up_tanks');
            $table->unsignedTinyInteger('signed_up_heals');
            $table->unsignedTinyInteger('signed_up_ranged_dps');
            $table->unsignedTinyInteger('signed_up_melee_dps');

            $table->foreign('event_id')->references('id')->on('events');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('event_rosters');
    }
}
