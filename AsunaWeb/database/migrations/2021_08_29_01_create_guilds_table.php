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
            $table->id();
            $table->timestamps();
            $table->string('guild_name', 100);
            $table->string('time_zone', 20)->default('UTC');
            $table->unsignedBigInteger('create_event_role');
            $table->unsignedBigInteger('admin_role');
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
