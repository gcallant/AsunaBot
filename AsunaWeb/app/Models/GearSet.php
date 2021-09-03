<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GearSet extends Model
{
    use HasFactory;

    protected $primaryKey = 'gearSetID';

    protected $fillable = [
        'gearSetName',
        'locationID'
    ];
}
