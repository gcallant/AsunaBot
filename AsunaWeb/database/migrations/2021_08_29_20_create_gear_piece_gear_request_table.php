<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateGearPieceGearRequestTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('gear_piece_gear_request', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->foreignId('gear_request_id');
            $table->foreignId('gear_piece_id');
            $table->boolean('is_active');

            $table->foreign('gear_request_id')->references('id')->on('gear_requests');
            $table->foreign('gear_piece_id')->references('id')->on('gear_pieces')->cascadeOnUpdate();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('gear_piece_gear_request');
    }
}
