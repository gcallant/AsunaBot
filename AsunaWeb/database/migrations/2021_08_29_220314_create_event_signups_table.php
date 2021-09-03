<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateEventSignupsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('event_signups', function (Blueprint $table)
        {
            $table->id('eventSignupID');
            $table->timestamps();
            $table->foreignId('eventID')->primary()->unique();
            $table->foreignId('guildMemberID');
            $table->foreignId('roleID');
            $table->foreignId('esoCharacterID');
            $table->boolean('noCallNoShow')->default(false);
            $table->string('guildMemberNotes', 1000)->nullable();

            $table->foreign('eventID')->references('eventID')->on('events');
            $table->foreign('guildMemberID')->references('guildMemberID')->on('guild_members')->cascadeOnDelete();
            $table->foreign('roleID')->references('roleID')->on('roles')->cascadeOnUpdate();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('event_signups');
    }
}
