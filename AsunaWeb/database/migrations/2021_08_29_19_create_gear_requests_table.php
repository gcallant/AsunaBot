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
            $table->id();
            $table->timestamps();
            $table->foreignId('guild_member_id');
            $table->foreignId('gear_set_id');

            $table->foreign('guild_member_id')->references('id')->on('guild_members');
            $table->foreign('gear_set_id')->references('id')->on('gear_sets')->cascadeOnUpdate();

            $table->unique(['guild_member_id', 'gear_set_id']);
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
