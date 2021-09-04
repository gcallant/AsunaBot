<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class EventData extends Model
{
    use HasFactory;

    protected $fillable = [
        'event_id',
        'event_day',
        'event_time',
        'event_description',
        'event_leader',
        'require_minimum_role',
        'minimum_role_id'
    ];

    protected $attributes = [
        'require_minimum_role' => false
    ];
}
