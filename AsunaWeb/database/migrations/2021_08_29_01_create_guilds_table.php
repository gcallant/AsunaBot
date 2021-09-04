<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateGuildsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('guilds', function (Blueprint $table)
        {
            $table->id('guildID');
            $table->timestamps();
            $table->string('guildName', 100);
            $table->string('timeZone', 20)->default('UTC');
            $table->unsignedBigInteger('createEventRole');
            $table->unsignedBigInteger('adminRole');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('guilds');
    }
}
