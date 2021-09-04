<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateEventsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('events', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->string('event_name', 200);
            $table->foreignId('event_type_id');
            $table->foreignId('guild_id');

            $table->foreign('guild_id')->references('id')->on('guilds')->cascadeOnDelete();
            $table->foreign('event_type_id')->references('id')->on('event_types')->cascadeOnUpdate();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('events');
    }
}
