<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GearRequest extends Model
{
    use HasFactory;

    protected $primaryKey = 'gearRequestedID';

    protected $fillable = [
        'guildMemberID',
        'gearSetID'
    ];
}
