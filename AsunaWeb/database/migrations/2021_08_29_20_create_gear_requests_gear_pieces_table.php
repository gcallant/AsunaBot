<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateGearRequestsGearPiecesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('gear_requests_gear_pieces', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->foreignId('gearRequestID');
            $table->foreignId('gearPieceID');

            $table->foreign('gearRequestID')->references('gearRequestID')->on('gear_requests');
            $table->foreign('gearPieceID')->references('gearPieceID')->on('gear_pieces')->cascadeOnUpdate();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('gear_requests_gear_pieces');
    }
}
