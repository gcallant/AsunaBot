<?php

namespace App\Http\Controllers;

use App\Models\Event;
use Illuminate\Http\JsonResponse;
use PHPUnit\Util\Json;

/**
 *
 */
class EventController extends Controller
{


    /**
     * @param Json $event_data
     * @return JsonResponse
     */
    public function create(Json $event_data) : JsonResponse
    {
        $event = Event::create($event_data);
        $event.update();

        return new JsonResponse($event, 200);
    }
}
