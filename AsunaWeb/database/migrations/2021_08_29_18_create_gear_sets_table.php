<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateGearSetsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('gear_sets', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->string('gear_set_name', 100);
            $table->foreignId('location_id');

            $table->foreign('location_id')->references('id')->on('locations')->cascadeOnUpdate();
            $table->unique(['gear_set_name', 'location_id']);
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('gear_sets');
    }
}
