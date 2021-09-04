<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateEventDataTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('event_data', function (Blueprint $table)
        {
            $table->id('eventDataID');
            $table->timestamps();
            $table->foreignId('eventID')->index()->unique();
            $table->date('eventDay');
            $table->timeTz('eventTime');
            $table->string('eventDescription', 2000);
            $table->foreignId('eventLeader');
            $table->boolean('requireMinimumRole')->default(false);
            $table->unsignedInteger('minimumRoleID')->nullable();

            $table->foreign('eventID')->references('eventID')->on('events')->cascadeOnUpdate();
            $table->foreign('eventLeader')->references('guildMemberID')->on('guild_members')->cascadeOnUpdate();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('event_data');
    }
}
