<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Guild extends Model
{
    use HasFactory;

    protected $primaryKey = 'guildID';
    public $incrementing = false;

    protected $attributes = [
        'timeZone' => 'UTC'
    ];

    protected $fillable = [
        'timeZone',
        'guildName'
    ];
}
