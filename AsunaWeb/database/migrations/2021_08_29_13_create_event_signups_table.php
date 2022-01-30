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
            $table->id();
            $table->timestamps();
            $table->foreignId('event_id')->unique();
            $table->foreignId('guild_member_id');
            $table->foreignId('role_id');
            $table->foreignId('eso_character_id');
            $table->boolean('no_call_no_show')->default(false);
            $table->string('guild_member_notes', 1000)->nullable();

            $table->foreign('event_id')->references('id')->on('events');
            $table->foreign('guild_member_id')->references('id')->on('guild_members')->cascadeOnDelete();
            $table->foreign('role_id')->references('id')->on('roles')->cascadeOnUpdate();
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
