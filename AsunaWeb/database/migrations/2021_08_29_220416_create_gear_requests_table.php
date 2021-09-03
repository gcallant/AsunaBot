<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateGearRequestsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('gear_requests', function (Blueprint $table)
        {
            $table->id('gearRequestID')->primary();
            $table->timestamps();
            $table->foreignId('guildMemberID');
            $table->foreignId('gearSetID');

            $table->foreign('guildMemberID')->references('guildMemberID')->on('guild_members');
            $table->foreign('gearSetID')->references('gearSetID')->on('gear_sets')->cascadeOnUpdate();

            $table->unique(['guildMemberID', 'gearSetID']);
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('gear_requests');
    }
}
