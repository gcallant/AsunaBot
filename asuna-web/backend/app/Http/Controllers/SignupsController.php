<?php

namespace App\Http\Controllers;

use App\Signup;
use App\Event;
use App\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Gate;
use App\Traits\Filterable;

class SignupsController extends Controller
{
    use Filterable;

    protected $resourceClass = Signup::class;

    public function __construct()
    {
      $this->guildRanks = config('enums.guildRanks');
    }

    /**
    * Get a list of signups for a particular event.
    *
    * @param int $id Event ID.
    * @return Illuminate\Https\Response
    */
    public function getByEvent($id)
    {
      $signups = Signup::where(['event_id' => $id])->get()->all();

      foreach($signups as $signup)
      {
        $signup->user = User::find($signup->player_id);
      }

      return response()->json(['signups' => $signups], 200);
    }

    /**
    * Get a list of signups for a particular user.
    *
    * @param int $id User ID.
    * @return Illuminate\Https\Response
    */
    public function getByUser($id)
    {
      $signups = Signup::where(['player_id' => $id])->get()->all();

      foreach($signups as $signup)
      {
        $signup->event = Event::find($signup->event_id);
      }

      return response()->json(['signups' => $signups], 200);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param string $id Event ID
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request, $id)
    {
      $event = Event::findOrFail($id);

      if(!$event->active){
        return response()->json(['error' => 'The event is inactive and does not allow signups.'], 403);
      }

      $request->request->set('event_id', $id);

      $user = Auth::guard('api')->user();

      // Only admins can signup on another user's behalf or override min_rank requirement.
      if (Gate::denies('is-admin')) {
        $request->request->set('player_id', $user->id);
        $request->request->set('admin_override', 0);
      }

      $switchedToReserveMessage = "";

      if($request->input('primary_role') != 'RESERVE') {

        // Enforce minimum rank requirement (unless overridden by admin).
        if(!$request->input('admin_override') && $this->guildRanks[$event->min_rank] < $this->guildRanks[$user->guild_rank])
        {
          $switchedToReserveMessage = "Minimum rank requirement not satisfied. Player signed up as RESERVE.";
        }

        // Enforce maximum role slots limit.
        elseif($event->getAttribute($request->input('primary_role')) == 0)
        {
          $switchedToReserveMessage = "Primary role is full. Player signed up as RESERVE.";
        }

        if($switchedToReserveMessage)
        {
          $request = $this->switchToReserve($request);
        }

        else
        {
          // Update open role slots in event.
          $event->{$request->input('primary_role')} -= 1;
        }
      }

      // Validate the user input
      $validator = Validator::make($request->all(), [
        'event_id' => ['required', 'exists:events,id'],
        'player_id' => ['required', 'exists:users,id'],
        'primary_role' => ['required', config('rules.isValidSignupRole')],
        'flex_roles' => ['nullable', config('rules.allValidSignupRoles')],
      ]);

      if($validator->fails()) {
        return response($validator->errors(), 400);
      }

      $signup = Signup::create($validator->validated());
      $event->save();

      return response()->json(['signup' => $signup, 'event' => $event, 'info' => $switchedToReserveMessage], 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  string $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        $signup = Signup::findOrFail($id);
        return response()->json(['signup' => $signup], 200);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Signup  $signup
     * @return \Illuminate\Http\Response
     */
    public function edit(Signup $signup)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, int $id)
    {
      $signup = Signup::findOrFail($id);
      $event = Event::findOrFail($request->input('event_id'));

      if(!$event->active){
        return response()->json(['error' => 'The event is inactive and does not allow signups.'], 403);
      }

      $user = Auth::guard('api')->user();

      // Only admins can signup on another user's behalf or override min_rank requirement.
      if (Gate::denies('is-admin')) {
        $request->request->set('admin_override', 0);
      }

      $switchedToReserveMessage = "";

      if($request->input('primary_role') != 'RESERVE') {

        // Enforce minimum rank requirement (unless overridden by admin).
        if(!$request->input('admin_override') && $this->guildRanks[$event->min_rank] < $this->guildRanks[$user->guild_rank])
        {
          $switchedToReserveMessage = "Minimum rank requirement not satisfied. Player signed up as RESERVE.";
        }

        // Enforce maximum role slots limit.
        elseif($event->getAttribute($request->input('primary_role')) == 0)
        {
          $switchedToReserveMessage = "Primary role is full. Player signed up as RESERVE.";
        }

        if($switchedToReserveMessage)
        {
          $request = $this->switchToReserve($request);
        }
      }

      // Validate the user input
      $validator = Validator::make($request->all(), [
        'primary_role' => ['required', config('rules.isValidSignupRole')],
        'flex_roles' => ['nullable', config('rules.allValidSignupRoles')],
      ]);


      if($validator->fails()) {
        return response($validator->errors(), 400);
      }

      if($request->input('primary_role') != $signup->primary_role)
      {
        // Update open role slots in event.
        if($request->input('primary_role') != 'RESERVE'){
          $event->{$request->input('primary_role')} -= 1;
        }
        
        if($signup->primary_role != 'RESERVE'){
          $event->{$signup->primary_role} += 1;
        }
      }

      $updatedSignup = $signup->update($validator->validated());
      $event->save();

      return response()->json(['signup' => $updatedSignup, 'event' => $event, 'info' => $switchedToReserveMessage], 200);

    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  string $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        $signup = Signup::findOrFail($id);

        if(Gate::denies('cancel-signup', $signup)){
          return response()->json(['error' => 'Not authorized to cancel this signup.'], 403);
        }

        if($signup->primary_role != 'RESERVE')
        {
          $event = Event::findOrFail($signup->event_id);
          $event->{$signup->primary_role} += 1;
          $event->save();
        }

        $signup->delete();

        return response()->json(['info' => 'Signup cancelled.'], 200);

    }

    /**
    * Switches primary role to RESERVE and places the desired role into flex roles.
    *
    * @param Request $request Original request.
    * @return Request Modified request.
    */
    protected function switchToReserve($request) {
      $desiredRole = $request->input('primary_role');
      $request->request->set('primary_role', 'RESERVE');
      if($request->has('flex_roles')) {
        $flexRoles = $desiredRole . ',' . $request->input('flex_roles');
        $request->request->set('flex_roles', $flexRoles);
      }
      else {
        $request->request->set('flex_roles', $desiredRole);
      }

      return $request;
    }


}
