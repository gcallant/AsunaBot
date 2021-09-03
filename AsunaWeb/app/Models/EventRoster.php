<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class EventRoster extends Model
{
    use HasFactory;

    protected $primaryKey = 'eventRosterID';

    protected $fillable = [
        'maxTanks',
        'maxHeals',
        'maxRangedDPS',
        'maxMeleeDPS'
    ];
}
