<?php

namespace App\Traits;

use App\Traits\ControlsModel;
use Illuminate\Support\Facades\Input;
use Illuminate\Support\Facades\Schema;

trait Filterable {

  use ControlsModel;

  /**
   * Display a listing of the resource, filtering results with GET parameters.
   *
   * @return \Illuminate\Http\Response
   */
  public function index()
  {
      // GET parameters
      $params = Input::all();

      $resource_name = $this->resourceModel();

      // Return all Resources if no GET parameters supplied.
      if(empty($params)){
        $resources = $resource_name::all();
        return response()->json(['data' => $resources], 200);
      }

      // Get the Resource fields that correspond to the supplied GET parameters
      $fields = array_intersect(array_keys($params), Schema::getColumnListing((new $resource_name())->getTable()));

      // Build WHERE filters based on the GET params.
      $filters = [];
      foreach($fields as $field){
          $filters[$field] = $params[$field];
      }

      $resources = $resource_name::where($filters)->get()->all();

      return response()->json(['data' => $resources], 200);
  }




}
