<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateESOUsersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('e_s_o_users', function (Blueprint $table)
        {
            $table->id('esoUserID')->primary();
            $table->timestamps();
            $table->string('familyName', 100);
            $table->foreignId('guilds_membersID');

            $table->foreign('guilds_membersID')->references('id')->on('guilds_guild_members');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('e_s_o_users');
    }
}
