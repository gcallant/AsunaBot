<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateGuildsGuildMembersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('guilds_guild_members', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->foreignId('guildID');
            $table->foreignId('guildMemberID');

            $table->foreign('guildID')->references('guildID')->on('guilds')->cascadeOnDelete();
            $table->foreign('guildMemberID')->references('guildMemberID')->on('guild_members')->cascadeOnDelete();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('guilds_guild_members');
    }
}
