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
    public function up(): void
    {
        Schema::create('e_s_o_users', function (Blueprint $table)
        {
            $table->id();
            $table->timestamps();
            $table->string('family_name', 100);
            $table->foreignId('guild_guild_member_id');

            $table->foreign('guild_guild_member_id')->references('id')->on('guild_guild_member');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down(): void
    {
        Schema::dropIfExists('e_s_o_users');
    }
}
