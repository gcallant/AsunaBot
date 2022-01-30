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
        Schema::create('guild_guild_member', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->foreignId('guild_id');
            $table->foreignId('guild_member_id');

            $table->foreign('guild_id')->references('id')->on('guilds')->cascadeOnDelete();
            $table->foreign('guild_member_id')->references('id')->on('guild_members')->cascadeOnDelete();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('guild_guild_member');
    }
}
