<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateUsersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table)
        {
            $table->id('userID')->primary();
            $table->timestamps();
            $table->foreignID('guildMemberID');
            $table->string('locale', 10);
            $table->string('timeZone', 20);
            $table->foreignId('themeID');
            $table->boolean('isAdmin')->default(false);

            $table->foreign('guildMemberID')->references('guildMemberID')->on('guildMembers');
            $table->foreign('themeID')->references('themeID')->on('themes');
        });

    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('users');
    }
}
