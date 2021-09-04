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
            $table->id('gearSetID');
            $table->timestamps();
            $table->string('gearSetName', 100);
            $table->foreignId('locationID');

            $table->foreign('locationID')->references('locationID')->on('locations')->cascadeOnUpdate();
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
