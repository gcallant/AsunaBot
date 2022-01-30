<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Facades\DB;

class LocationType extends Model
{
    use HasFactory;

    protected $fillable = [
        'type_name',
    ];

    public static function getID(string $str_replace) : int
    {
        return DB::table('location_types')->where('type_name', $str_replace)->value('id');
    }

    public function location() : HasMany
    {
        return $this->hasMany(Location::class);
    }
}
