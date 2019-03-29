<?php

namespace App\Http\Controllers;

use App\Event;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Gate;

class EventsController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $events = \App\Event::all();
        return response()->json(['events' => $events], 200);
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        if (Gate::denies('create-event')) {
          return response()->json(['error' => 'Not authorized to create events.'], 403);
        }


        $user = Auth::guard('api')->user();

        $request->request->set('created_by_id', $user->discord_id);

        $validator = Validator::make($request->all(), [
          'event_name' => ['required', 'max:20'],
          'trial_name' => ['nullable', 'max:20'],
          'event_time' => ['required', 'date', 'after:now'],
          'created_by_id' => ['required'],
          'event_leader' => ['required', 'exists:users,discord_id'],
          'active' => ['nullable', 'boolean'],
          'description' => ['required', 'min:3', 'max:250'],
          'min_rank' => ['required'],
          'channel_info_message' => ['nullable'],
        ]);

        if($validator->fails()) {
          return response($validator->errors(), 400);
        }

        $event = Event::create($validator->validated());

        return response()->json(['event' => $event], 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
