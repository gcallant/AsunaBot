<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateEventDataTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('event_data', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->foreignId('event_id')->index()->unique();
            $table->date('event_day');
            $table->timeTz('event_time');
            $table->string('event_description', 2000);
            $table->foreignId('event_leader');
            $table->boolean('require_minimum_role')->default(false);
            $table->unsignedInteger('minimum_role_id')->nullable();

            $table->foreign('event_id')->references('id')->on('events')->cascadeOnUpdate();
            $table->foreign('event_leader')->references('id')->on('guild_members')->cascadeOnUpdate();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('event_data');
    }
}
