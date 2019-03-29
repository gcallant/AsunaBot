<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateEventsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('events', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('channel_id')->nullable();
            $table->string('event_name');
            $table->string('trial_name')->nullable();
            $table->DateTime('event_time');
            $table->string('created_by_id');
            $table->string('event_leader');
            $table->boolean('active')->default(True);
            $table->string('description');
            $table->string('min_rank');
            $table->string('channel_info_message')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('events');
    }
}
