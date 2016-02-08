//
//  SecondViewController.swift
//  TankPi
//
//  Created by Kevin McGill on 1/31/16.
//  Copyright © 2016 Kevin McGill. All rights reserved.
//

import UIKit

class SecondViewController: BaseViewController, HTTPsterDelegate {

    
    let url = NSURL(string: "https://tankpi.mcgilln.com/tankpi.php")
    var headers = ["Authorization":"Basic a2V2bzpiYW5hbmFz"]
    
    
    
    
    @IBOutlet weak var whiteon: UIButton!
    @IBOutlet weak var blueon: UIButton!
    @IBOutlet weak var moonon: UIButton!
    
    @IBOutlet weak var whiteoff: UIButton!
    @IBOutlet weak var blueoff: UIButton!
    @IBOutlet weak var moonoff: UIButton!
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        //Make delegate
        HTTPster.shared.delegate = self

    }

    
    @IBAction func on(sender: UIButton) {
        
        var postBody = ""
        
        if sender == whiteon {
            postBody = "white=on"
        } else if sender == blueon {
            postBody = "blue=on"
        } else {
            postBody = "moon=on"
        }
        
        
        HTTPster.shared.makeRequest("OnLight", httpType: HTTPster.HTTPMethod.POST, contentType: HTTPster.HTTPContentType.URL_ENCODED, url: url!, headers: headers, postBody: postBody)
        print(postBody)
        
    }
    
    @IBAction func off(sender: UIButton) {
        
        var postBody = ""
        
        if sender == whiteoff {
            postBody = "white=off"
        } else if sender == blueoff {
            postBody = "blue=off"
        } else {
            postBody = "moon=off"
        }
        
        HTTPster.shared.makeRequest("OffLight", httpType: HTTPster.HTTPMethod.POST, contentType: HTTPster.HTTPContentType.URL_ENCODED, url: url!, headers: headers, postBody: postBody)
        print(postBody)
        
    }
    
    func didRetrieveResponse(tag: Any, response: NSURLResponse?, responsedata: NSData?, error: NSError?) {

        if let goodTag = tag as? String {
            if goodTag == "OffLight" || goodTag == "OnLight" {
                var message = ""
                
                if let httpResponse = response as? NSHTTPURLResponse {
                    print("Status code: (\(httpResponse.statusCode))")
                    message += "Status code: \(httpResponse.statusCode)"
                }
                
                if let goodData = responsedata {
                    let tempResponse = NSString(data: goodData, encoding: NSUTF8StringEncoding)
                    if let goodResponse = tempResponse {
                        message += " \nLight Status: \(goodResponse)"
                    }
                    
                }
                
                showAlertWithMessage("Alert", message: message, action: UIAlertAction(title: "Dismiss", style: .Default, handler: nil))
            }
        }
    }

}

