<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateGuildMembersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('guild_members', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->string('name', 100);
            $table->unsignedBigInteger('discord_user_id');
            $table->json('discord_role_ids');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('guild_members');
    }
}
