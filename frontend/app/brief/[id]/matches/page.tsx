'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { matchingApi, type VenueMatch } from '@/lib/api/matching'
import { Button } from '@/components/ui/button'
import { MapPin, Users, DollarSign, Star, ArrowLeft, Loader2 } from 'lucide-react'

export default function MatchResultsPage() {
  const params = useParams()
  const router = useRouter()
  const [matches, setMatches] = useState<VenueMatch[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    const loadMatches = async () => {
      try {
        const briefId = parseInt(params.id as string)
        const data = await matchingApi.getMatches(briefId)

        if (data.matches.length === 0 && data.message) {
          // No matches yet - trigger generation
          setGenerating(true)
          await matchingApi.generateMatches(briefId)
          // Wait a bit and retry
          setTimeout(async () => {
            const retryData = await matchingApi.getMatches(briefId)
            setMatches(retryData.matches)
            setGenerating(false)
            setLoading(false)
          }, 3000)
        } else {
          setMatches(data.matches)
          setLoading(false)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load matches')
        setLoading(false)
      }
    }

    loadMatches()
  }, [params.id])

  const formatBorough = (borough: string) => {
    return borough
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400'
    if (score >= 60) return 'text-blue-600 dark:text-blue-400'
    if (score >= 40) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-gray-600 dark:text-gray-400'
  }

  const getScoreBadge = (score: number) => {
    if (score >= 80) return 'Excellent Match'
    if (score >= 60) return 'Good Match'
    if (score >= 40) return 'Decent Match'
    return 'Possible Match'
  }

  if (loading || generating) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">
            {generating ? 'Finding your perfect venues...' : 'Loading matches...'}
          </h2>
          <p className="text-muted-foreground">
            {generating
              ? 'Our AI is analyzing venues across NYC'
              : 'This will just take a moment'}
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-destructive mb-4">{error}</p>
          <Button onClick={() => router.push('/host/dashboard')}>
            Back to Dashboard
          </Button>
        </div>
      </div>
    )
  }

  if (matches.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">No matches found</h2>
          <p className="text-muted-foreground mb-6">
            We couldn't find any venues that match your requirements.
            Try adjusting your brief criteria.
          </p>
          <Button onClick={() => router.push(`/brief/${params.id}`)}>
            Edit Brief
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 bg-background border-b z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => router.push(`/brief/${params.id}`)}
            className="mb-2"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Brief
          </Button>
          <h1 className="text-2xl font-bold">Your Venue Matches</h1>
          <p className="text-muted-foreground">
            {matches.length} venues ranked by how well they fit your event
          </p>
        </div>
      </div>

      {/* Matches list */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="space-y-6">
          {matches.map((match) => (
            <div
              key={match.match_id}
              className="bg-card border rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
            >
              {/* Rank badge */}
              <div className="bg-primary/10 px-6 py-3 flex items-center justify-between border-b">
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold">
                    {match.rank}
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold">{match.venue.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      {formatBorough(match.venue.borough)}
                      {match.venue.neighborhood && `, ${match.venue.neighborhood}`}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${getScoreColor(match.score)}`}>
                    {match.score.toFixed(0)}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {getScoreBadge(match.score)}
                  </div>
                </div>
              </div>

              <div className="p-6">
                {/* Description */}
                {match.venue.description && (
                  <p className="text-muted-foreground mb-4">
                    {match.venue.description}
                  </p>
                )}

                {/* Quick facts */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                  <div className="flex items-center gap-2">
                    <Users className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm">
                      {match.venue.capacity_min}-{match.venue.capacity_max} guests
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm truncate">{match.venue.address}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <DollarSign className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm">
                      {match.venue.base_price
                        ? `$${match.venue.base_price}+`
                        : match.venue.min_spend
                        ? `$${match.venue.min_spend} min`
                        : 'Contact for pricing'}
                    </span>
                  </div>
                </div>

                {/* Why it matches */}
                <div className="bg-muted/50 rounded-lg p-4 mb-4">
                  <div className="flex items-start gap-2 mb-2">
                    <Star className="w-5 h-5 text-primary mt-0.5" />
                    <h4 className="font-semibold">Why this venue matches</h4>
                  </div>
                  <div
                    className="text-sm prose prose-sm dark:prose-invert max-w-none"
                    dangerouslySetInnerHTML={{
                      __html: match.explanation.replace(/\n/g, '<br/>'),
                    }}
                  />
                </div>

                {/* Actions */}
                <div className="flex gap-3">
                  <Button
                    onClick={() => router.push(`/venue/${match.venue.id}`)}
                    className="flex-1"
                  >
                    View Details
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() =>
                      router.push(`/brief/${params.id}/venue/${match.venue.id}/request-offer`)
                    }
                    className="flex-1"
                  >
                    Request Offer
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
