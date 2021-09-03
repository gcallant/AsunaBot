<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class EventData extends Model
{
    use HasFactory;

    protected $primaryKey = 'eventDataID';

    protected $fillable = [
        'eventID',
        'eventDay',
        'eventTime',
        'eventDescription',
        'eventLeader',
        'requireMinimumRole',
        'minimumRoleID'
    ];

    protected $attributes = [
        'requireMinimumRole' => false
    ];
}
