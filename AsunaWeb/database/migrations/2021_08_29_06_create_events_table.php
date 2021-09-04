<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateEventsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('events', function (Blueprint $table)
        {
            $table->id('eventID');
            $table->timestamps();
            $table->string('eventName', 200);
            $table->foreignId('eventTypeID');
            $table->foreignId('guildID');

            $table->foreign('guildID')->references('guildID')->on('guilds')->cascadeOnDelete();
            $table->foreign('eventTypeID')->references('eventTypeID')->on('event_types')->cascadeOnUpdate();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('events');
    }
}