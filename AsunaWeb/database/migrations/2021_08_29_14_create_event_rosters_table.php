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
            $table->id('eventRosterID');
            $table->timestamps();
            $table->foreignId('eventID')->unique();
            $table->unsignedTinyInteger('maxTanks')->nullable();
            $table->unsignedTinyInteger('maxHeals')->nullable();
            $table->unsignedTinyInteger('maxRangedDPS')->nullable();
            $table->unsignedTinyInteger('maxMeleeDPS')->nullable();
            $table->unsignedTinyInteger('signedUpTanks');
            $table->unsignedTinyInteger('signedUpHeals');
            $table->unsignedTinyInteger('signedUpRangedDPS');
            $table->unsignedTinyInteger('signedUpMeleeDPS');

            $table->foreign('eventID')->references('eventID')->on('events');
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
