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
    public function up()
    {
        Schema::create('guilds_guild_members', function (Blueprint $table)
        {
            $table->id()->primary();
            $table->timestamps();
            $table->foreignId('guildID');
            $table->foreignId('guildMemberID');

            $table->foreign('guildID')->references('guildID')->on('Guilds')->cascadeOnDelete();
            $table->foreign('guildMemberID')->references('guildMemberID')->on('GuildMembers')->cascadeOnDelete();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('guilds_guild_members');
    }
}
