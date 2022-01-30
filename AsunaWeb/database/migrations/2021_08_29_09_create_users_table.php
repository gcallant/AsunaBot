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
            $table->id();
            $table->timestamps();
            $table->foreignID('guild_member_id');
            $table->string('locale', 10);
            $table->string('time_zone', 20);
            $table->foreignId('theme_id');
            $table->boolean('is_admin')->default(false);

            $table->foreign('guild_member_id')->references('id')->on('guild_members');
            $table->foreign('theme_id')->references('id')->on('themes');
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
