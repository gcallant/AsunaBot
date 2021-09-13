<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Facades\DB;

class Location extends Model
{
    use HasFactory;

    protected $fillable = [
        'location_name',
        'location_type_id'
    ];

    public static function getID(string $name, int $typeID) : int
    {
        return DB::table('locations')
                 ->where('location_name', $name)
                 ->where('location_type_id', $typeID)
                 ->value('id');
    }

    public function locationType() : BelongsTo
    {
        return $this->belongsTo(LocationType::class);
    }
}
